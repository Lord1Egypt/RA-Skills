import MonthInput from "/assets/v3/components/month_input.js"

export default {
inject:['service', 'tags'],
components:{
    "month-input":MonthInput
},
data() {return {
    salaries:{}, //发薪申请uid,post,account,name,phone,val
    salPg:{max:0,cur:1},
    salAct:{dlg:false,dtl:{},sal:{}},
    month:'-1m'
}},
created(){
    this.query(1);
},
methods:{
query(pg) {
    this.query_employees(pg).then(sals=> {
        this.query_sals(); 
    });
},
query_employees(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url="/employee/simpleListAll?offset="+offset+"&num="+this.service.N_PAGE;
    return request({method:"GET", url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return [];
        }
        var cols=resp.data.cols;
        var sals={};
        var sal;
        var staInit=this.tags.aplSta['INIT'];
        for(var l of resp.data.list) {
            sal={state:'INIT',state_s:staInit};
            for(var i in cols) {
                sal[cols[i]]=l[i];
            }
            sals[sal.uid]=sal;
        }
        this.salaries=sals;
        return sals;
    })
},
query_sals() {
    var uids=[];
    for(var uid in this.salaries) {
        uids.push(uid);
    }
    var dta={month:this.month.num,uids:uids};
    request({method:"POST", url:'/salary/list', data:dta}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            for(var uid in this.salaries) {
                this.salaries[uid].val=0;
            }
            return;
        }
        var dt=new Date();
        for(var l of resp.data.list) {
            var sal=this.salaries[l[0]];
            sal.val=l[1];
            dt.setTime(l[2]);
            sal.state_s=this.tags.aplSta[l[3]];
            sal.state=l[3];
            sal.cfmAt=datetime2str(dt);
        }
    })
},
show_dtl(uid) {
    var url='/salary/detail?uid='+uid+'&month='+this.month.num;
    request({method:"GET", url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var pos;
        for(var o of resp.data.salaries) {
            pos=o.type.indexOf('-');
            if(pos>0) {
                o.type=this.tags.salTp[o.type.substring(0,pos)]
                   + '('+this.tags.sponTp[o.type.substring(pos+1)]+')';
            } else {
                o.type=this.tags.salTp[o.type];
            }
            o.val=o.val.toFixed(2);
        }
        this.salAct.dtl=resp.data;
        this.salAct.sal=this.salaries[uid];
        this.salAct.dlg=true;
    })
},
sal_confirm() {
    var dta={month:this.month.num,uid:this.salAct.sal.uid};
    request({method:"POST", url:"/salary/confirm", data:dta}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.salAct.dlg=false;
        this.query_sals();
    });
},
set_month() {
    this.query_sals();
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.salary.title}}</q-toolbar-title>
     <month-input class="text-subtitle1 q-pl-sm" v-model="month"
      @update:modelValue="set_month" min="-3" max="-1m"></month-input>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list separator>
  <q-item v-for="(s,uid) in salaries" clickable @click="show_dtl(uid)">
    <q-item-section>
     <q-item-label>{{s.account}}</q-item-label>
     <q-item-label caption>{{s.name}}</q-item-label>
    </q-item-section>
    <q-item-section side>
     <q-item-label>{{s.val}}({{s.state_s}})</q-item-label>
     <q-item-label caption>{{s.cfmAt}}</q-item-label>
    </q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="salPg.max>1">
 <q-pagination v-model="salPg.cur" color="primary" :max="salPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
    </q-page>
  </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>

<q-dialog v-model="salAct.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{salAct.sal.name}}/{{salAct.sal.account}}</div>
   <div class="text-caption">{{salAct.dtl.path}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-list separator>
    <q-item v-for="s in salAct.dtl.salaries">
     <q-item-section>{{s.type}}</q-item-section>
     <q-item-section side>{{s.val}}</q-item-section>
    </q-item>
   </q-list>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="sal_confirm"
     v-if="salAct.sal.state!='OK'"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>
`
}