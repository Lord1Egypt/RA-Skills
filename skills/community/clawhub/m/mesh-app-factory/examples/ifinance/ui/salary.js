export default {
inject:['service', 'tags'],
data() {return {
    list:{}, //发薪申请
    ctrl:{max:0,cur:1,dlg:false,dta:{},month:"-1m",state:'',opts:[]},
    download:{dlg:false,list:[]}
}},
created(){
    var opts=[{value:'',label:this.tags.unSet}];//状态选择项
    for(var i in this.tags.salary.state){
        opts.push({value:i,label:this.tags.salary.state[i]});
    }
    this.ctrl.opts=opts;
    this.query(1);
},
methods:{
query(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url="/salary/list?offset="+offset+"&num="+this.service.N_PAGE
            +"&month="+this.ctrl.month.num+"&state="+this.ctrl.state;
    request({method:"GET", url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        //uid,mode,state,applyAt,account,cmt
        var vals=resp.data.vals;
        var dt=new Date();
        var states=this.tags.salary.state;
        var modes=this.tags.payMode;
        this.list=resp.data.list.map(l=>{
            dt.setTime(l.applyAt*60000);
            l.applyAt=datetime2str(dt);
            l.mode=modes[l.mode];
            l.state_s=states[l.state];
            l.val=vals[l.uid] ? vals[l.uid] : 0;
            return l;
        });
        //服务侧不返回total，max为NaN，因为max改变，所以触发q-pagination
        //导致调用query(NaN)。此问题在多个地方出现过
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
show_dtl(uid) {
    var url='/salary/get?uid='+uid+'&month='+this.ctrl.month.num;
    request({method:"GET", url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var dta=resp.data;
        var salTypes=this.tags.salaryType;
        var v,total=0;
        var pos,type_s;
        var items=[];
        for(var k in dta.items){
            v=dta.items[k];
            total+=v;
            
            pos=k.indexOf('-');
            if(pos>0) {
                type_s=salTypes[k.substring(0,pos)]
                   + '('+this.tags.sponTp[k.substring(pos+1)]+')';
            } else {
                type_s=salTypes[k];
            }
            items.push({type_s:type_s,type:k,val:v.toFixed(2)});
        }
        total=total.toFixed(2);
        //state,mode,applyAt,payAt,account,cfmAcc,cmt
        var dt=new Date();
        dt.setTime(dta.applyAt*60000);
        dta.applyAt=datetime2str(dt);
        if(dta.payAt>0) {
            dt.setTime(dta.payAt*60000);
            dta.payAt=datetime2str(dt);
        } else {
            dta.payAt=this.tags.notPaid;
        }
        dta.state_s=this.tags.salary.state[dta.state];
        if(!dta.bank)dta.bank={};
        dta.uid=uid;

        this.ctrl.dta=dta;
        this.ctrl.dta.items=items;
        this.ctrl.dta.total=total;
        request({method:"GET", url:"/getName?uid="+uid}, SERVICE_USER).then(resp => {
            if(resp.code==RetCode.OK) {
                this.ctrl.dta.name=resp.data.nickName;
            }
            this.ctrl.dlg=true;
        })        
    })
},
sal_confirm() {
    var dta={month:this.ctrl.month.num,
        uid:this.ctrl.dta.uid,
        mode:this.ctrl.dta.mode};
    request({method:"PUT", url:"/salary/confirm", data:dta}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.dlg=false;
        this.query(this.ctrl.cur);
    });
},
set_month() {
    this.query(this.ctrl.cur)
},
dl_salary() {
    var dt=new Date();
    var fn='salary_'+dt.getFullYear()+ String(dt.getMonth()).padStart(2, '0')
        +String(dt.getDate()).padStart(2, '0')+".xlsx";
    var url='/api/salary/download?month=' + this.ctrl.month.num
        + "&state=" + this.ctrl.state;
    download({file_name:fn, url:url, timeout:30000}, this.service.name).then(resp => {
        if(resp.code == RetCode.OK) {
            this.download.list.splice(0,0,{file:resp.data.saveAs, size:resp.data.size, bg:'#00000000'})
        } else {
            this.download.list.splice(0,0,{file:fn, size:0, bg:'#884444'})
        }
        this.download.dlg=true;
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.salary.title}}</q-toolbar-title>
     <month-input class="text-subtitle1 q-pl-sm" v-model="ctrl.month"
      @update:modelValue="set_month" min="-3" max="-1m"></month-input>
     <q-btn flat round dense icon="menu">
      <q-menu>
       <q-option-group v-model="ctrl.state" :options="ctrl.opts" type="radio"
       @update:model-value="query(ctrl.cur)" style="min-width:10em;"></q-option-group>
       <q-separator></q-separator>
       <q-btn :label="tags.salary.download" @click="dl_salary"
        flat color="primary" icon="get_app"></q-btn>
      </q-menu>
     </q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list separator>
  <q-item v-for="s in list" clickable @click="show_dtl(s.uid)">
    <q-item-section>
     <q-item-label>{{s.account}}</q-item-label>
     <q-item-label caption>{{s.applyAt}}</q-item-label>
    </q-item-section>
    <q-item-section>{{s.val}}</q-item-section>
    <q-item-section side :class="s.state=='OVER'?'text-grey':'text-primary'">{{s.state_s}}</q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
    </q-page>
  </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>

<q-dialog v-model="ctrl.dlg" persistent>
 <q-card style="min-width:70vw">
  <q-card-section class="q-pb-none">
   <div class="text-h6">{{ctrl.dta.account}}({{ctrl.dta.state_s}})</div>
   <div class="text-caption">{{ctrl.dta.name}}</div>
  </q-card-section>
  <hr>
  <q-card-section>
   <q-list dense separator>
    <q-item>
     <q-item-section>{{tags.applyAt}}</q-item-section>
     <q-item-section>{{ctrl.dta.applyAt}}</q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.payAt}}</q-item-section>
     <q-item-section>{{ctrl.dta.payAt}}</q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.salary.cfmAcc}}</q-item-section>
     <q-item-section>{{ctrl.dta.cfmAcc}}</q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.cmt}}</q-item-section>
     <q-item-section>{{ctrl.dta.cmt}}</q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.salary.bank}}</q-item-section>
     <q-item-section>
      <q-item-label>{{ctrl.dta.bank.bank}}</q-item-label>
      <q-item-label>{{ctrl.dta.bank.account}}</q-item-label>
      <q-item-label>{{ctrl.dta.bank.name}}</q-item-label>
     </q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.salary.total}}</q-item-section>
     <q-item-section>{{ctrl.dta.total}}</q-item-section>
    </q-item>
   </q-list>   
   <q-list dense separator>
    <q-item v-for="i in ctrl.dta.items">
     <q-item-section>{{i.type_s}}</q-item-section>
     <q-item-section side>{{i.val}}</q-item-section>
    </q-item>
   </q-list>
   <q-option-group v-model="ctrl.dta.mode" :options="ctrl.opts"
    inline type="radio" v-if="ctrl.dta.state=='WAIT'"></q-option-group>
  </q-card-section>
  <hr>
  <q-card-actions align="right" class="q-pt-none">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="sal_confirm"
     v-if="ctrl.dta.state=='WAIT'"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="download.dlg">
<q-card style="min-width:60vw;max-width:90vw">
<q-card-section class="row items-center q-pb-none">
  <div class="text-h6">{{tags.salary.dlList}}</div>
  <q-space></q-space>
  <q-btn icon="close" flat round dense v-close-popup></q-btn>
</q-card-section>
<q-card-section>
 <q-markup-table style="width:100%;" flat>
  <tr v-for="l in download.list" :style="{'background-color':l.bg}">
   <td>{{l.file}}</td>
   <td>{{l.size}}</td>
  </tr>
 </q-markup-table>
</q-card-section>
</q-card>
</q-dialog>
`
}