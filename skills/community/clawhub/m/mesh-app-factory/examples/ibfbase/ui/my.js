import AlertDialog from "/assets/v3/components/alert_dialog.js"
import MonthInput from "/assets/v3/components/month_input.js"
const RT_TAB="mytab";

export default {
inject:["ibf"],
components:{
    "alert-dialog":AlertDialog,
    "month-input":MonthInput
},
data() {return {
    tags:this.ibf.tags,
    tab:'', //event,salary,res,perf
    events:[],
    res:[],
    info:{securities:{}},
    perfs:[],
    salaries:[],
    salMonth:"-1m",
    evtPg:{cur:1,max:0},
    perfPg:{cur:1,max:0},
    resCtrl:{cur:1,max:0,dlg:false,no:'',logs:[],move:'',user:[]}
}},
created(){
    this.tab=this.ibf.getRt(RT_TAB,'base');
    if(this.tab!='base') { //salMonth会自动出发一次
        this.tab_changed(this.tab);
    }
    this.query_my();
},
methods:{
query_salary(ym) {
    request({method:"GET",url:"/salary/my?month="+ym.num}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.salaries=[];
            return;
        }
        var salTps=this.tags.hr.salType;
        var sponTps=this.tags.hr.sponTp;
        this.salaries=resp.data.list.map(s => {
            var pos=s.type.indexOf('-');
            var type;
            if(pos>0) {
                type=salTps[s.type.substring(0,pos)]
                  + '('+sponTps[s.type.substring(pos+1)]+')';
            } else {
                type=salTps[s.type];
            }
            return {val:s.val.toFixed(2),type:type};
        })
    })
},
query_my() {
    request({method:"GET",url:"/employee/my"}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.info={securities:{}};
            return;
        }
        var salTps=this.tags.hr.salType;
        var secTps=this.tags.hr.secType;
        var sponTps=this.tags.hr.sponTp;
        var dt=new Date();
        dt.setTime(resp.data.entryAt*60000);
        resp.data.entryAt=date2str(dt);
        resp.data.sickRatio=(resp.data.sickRatio*100)+'%';
        resp.data.attend=this.tags.hr.attendTp[resp.data.attend];
        this.info=resp.data;
        this.info.securities=resp.data.securities.map(s => {
            s.sponsor=sponTps[s.sponsor];
            if(s.type=='R') {
                s.val=(s.val*100).toFixed(2)+'%';
            }
            s.type=secTps[s.type];
            s.name=salTps[s.name];
            return s;
        })
    })
},
query_event(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/event/my?offset="+offset+'&num='+this.ibf.N_PAGE;
    request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.evtPg.max=0;
            this.evtPg.cur=1;
            this.events=[];
            return;
        }
        var evtTypes=this.tags.hr.eventType;
        //at,type,val,cmt
        var dt=new Date();
        this.events=resp.data.list.map(s => {
            var type=evtTypes[s.type];
            s.type=type?type:s.type;
            dt.setTime(s.at*60000);
            s.at=date2str(dt);
            return s;
        });
        this.evtPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    });    
},
query_res(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/resource/my?offset="+offset+'&num='+this.ibf.N_PAGE;
    request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.resCtrl.max=0;
            this.resCtrl.cur=1;
            this.res=[];
            return;
        }
        var dt=new Date(); //start,no,cfmAt,skuName
        this.res=resp.data.list.map(r => {
            dt.setTime(r.start*60000);
            r.start=date2str(dt);
            dt.setTime(r.inDate*60000); //第一次入库日期
            r.inDate=date2str(dt);
            return r;
        });
        this.resCtrl.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    });    
},
query_perf(pg) {
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url="/perf/my?offset="+offset+'&num='+this.ibf.N_PAGE;
    request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.perfPg.max=0;
            this.perfPg.cur=1;
            this.perfs=[];
            return;
        }
        //month,level,cmt,cfmed
        this.perfs=resp.data.list.map(p => {
            var m=p.month%12+1;
            p.month=parseInt(p.month/12)+'/'+(m<10?'0'+m:m);
            p.state=p.cfmed=='Y'?this.tags.hr.cfmed:this.tags.hr.notCfm;
            return p;
        });
        this.perfPg.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    });    
},
tab_changed(tab) {
    this.ibf.setRt(RT_TAB, tab);
    if(tab=='res') {
        if(this.res.length==0) {
            this.query_res(this.resCtrl.cur);
        }
    } if(tab=='event') {
        if(this.events.length==0) {
            this.query_event(this.evtPg.cur);
        }
    } else if(tab=='base') {
        if(this.salaries.length==0) {
            this.query_salary(this.salMonth);
        }
    } else if(tab=='perf'){
        if(this.perfs.length==0) {
            this.query_perf(this.perfPg.cur);
        }
    }
},
open_grp(id,type) {
    if(type=='D') {//业务部门
        this.ibf.goto('/ibf/department?id='+id);
    } else { //虚拟组织
        this.ibf.goto('/ibf/grp?id='+id);
    }
},
show_logs(no) {
    this.query_logs(no).then(()=>{
        this.resCtrl.dlg=true;
        this.resCtrl.no=no;
    }); 
},
query_logs(no) {
    var url="/resource/logs?no="+no;
    return request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.resCtrl.logs=[];
            return;
        }
        var dt=new Date();
        this.resCtrl.logs=resp.data.list.map(l => {
            dt.setTime(l.start*60000);
            l.start=date2str(dt);
            if(l.end==2147483647) {
                l.end=this.tags.my.now;
            } else {
                dt.setTime(l.end*60000);
                l.end=date2str(dt);
            }
            return l;
        });
        this.resCtrl.move=resp.data.moveFrom;
    });    
},
move_to(){
    var opts={method:"PUT",url:"/resource/moveto",
        data:{no:this.resCtrl.no,receiver:this.resCtrl.user[0]}};
    request(opts, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.resCtrl.dlg=false;
        this.query_res(this.resCtrl.cur);
    });    
},
accept_move() {
    var opts={method:"PUT",url:"/resource/accept", data:{no:this.resCtrl.no}};
    request(opts, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query_logs(this.resCtrl.no);
    });    
},
reject_move() {
    var opts={method:"PUT",url:"/resource/reject", data:{no:this.resCtrl.no}};
    request(opts, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.resCtrl.dlg=false;
        this.query_res(this.resCtrl.cur);
    });    
},
set_contact(v, _v0) {//修改联系方式
    var dta={phone:v.phone, email:v.email};
    request({method:"PUT", url:"/api/employee/update", data:dta}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.info.email=v.email;
        this.student.phone=v.phone;
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.my.title}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-footer>
   <q-tabs v-model="tab" @update:model-value="tab_changed" dense align="justify" switch-indicator inline-label
    class="text-grey bg-grey-3" active-color="primary" indicator-color="primary">
    <q-tab name="base" icon="info" :label="tags.my.base"></q-tab>
    <q-tab name="perf" icon="autofps_select" :label="tags.my.perm"></q-tab>
    <q-tab name="res" icon="devices" :label="tags.my.res"></q-tab>
    <q-tab name="event" icon="receipt_long" :label="tags.my.event"></q-tab>
   </q-tabs>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-none">
<q-tab-panels v-model="tab">

<q-tab-panel name="base">
<q-list separator dense>
 <q-item>
  <q-item-section>
    <div>
     {{info.email}}/{{info.phone}}
     <q-icon name="edit" color="primary"></q-icon>
    </div>
    <q-popup-edit v-model="info" auto-save buttons v-slot="scope"
     @save="set_contact" :label-set="tags.save" :label-cancel="tags.cancel">
     <q-input v-model="scope.value.email" dense></q-input>
     <q-input v-model="scope.value.phone" dense></q-input>
    </q-popup-edit>
  </q-item-section>
  <q-item-section>{{info.office}}({{info.zName}})/{{info.worktime}}</q-item-section>
 </q-item>
 <q-item>
  <q-item-section>
   <q-item-label caption>{{tags.hr.quali}}:{{info.quali}}</q-item-label>
   <q-item-label caption>{{tags.hr.post}}:{{info.post}}</q-item-label>
   <q-item-label caption>{{tags.hr.salary}}:{{info.salary}}</q-item-label>
   <q-item-label caption>{{tags.hr.subsidy}}:{{info.subsidy}}</q-item-label>
   <q-item-label caption>{{tags.hr.attend}}:{{info.attend}}</q-item-label>
   <q-item-label caption>
   {{tags.hr.entryAt}}:{{info.entryAt}}
    <q-badge color="primary" @click="ibf.goto('/ibf/resume?uid='+ibf.userInfo.id)">
     {{tags.resume.title}}<q-icon name="event_note" color="white"></q-icon>
    </q-badge>
   </q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label caption>{{tags.hr.holiday}}:{{info.holiday}}</q-item-label>
   <q-item-label caption>{{tags.hr.weal}}:{{info.weal}}</q-item-label>
   <q-item-label caption>{{tags.hr.sickRatio}}:{{info.sickRatio}}</q-item-label>
   <q-item-label caption>{{tags.hr.fowSalary}}:{{info.fowSalary}}</q-item-label>
   <q-item-label caption>{{tags.hr.oowSalary}}:{{info.oowSalary}}</q-item-label>
   <q-item-label caption>{{tags.hr.wowSalary}}:{{info.wowSalary}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
<q-banner dense inline-actions class="q-mb-md text-dark bg-blue-grey-1" dense>
{{tags.hr.security}}
</q-banner>
<q-list separator dense>
 <q-item v-for="s in info.securities">
  <q-item-section>{{s.name}}</q-item-section>
  <q-item-section>{{s.sponsor}}</q-item-section>
  <q-item-section>{{s.type}}</q-item-section>
  <q-item-section>{{s.val}}</q-item-section>
 </q-item>
</q-list>
<q-banner dense inline-actions class="q-mb-md text-dark bg-blue-grey-1" dense>
{{tags.my.monSalary}}
  <template v-slot:action>
   <month-input class="justify-right text-primary" min="-3" max="cur"
    v-model="salMonth" @update:modelValue="query_salary"></month-input>
  </template>
</q-banner>
<q-list separator dense>
 <q-item v-for="s in salaries">
  <q-item-section>{{s.type}}</q-item-section>
  <q-item-section>{{s.val}}</q-item-section>
 </q-item>
</q-list>
</q-tab-panel>

<q-tab-panel name="perf">
 <q-list separator dense>
  <q-item v-for="p in perfs">
   <q-item-section>{{p.month}}</q-item-section>
   <q-item-section>{{p.level}}-</q-item-section>
   <q-item-section>{{p.state}}:{{p.cmt}}</q-item-section>
  </q-item>
 </q-list>
 <div class="q-pa-sm flex flex-center" v-show="perfPg.max>1">
  <q-pagination v-model="perfPg.cur" color="primary" :max="perfPg.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_perf"></q-pagination>
 </div>
</q-tab-panel>

<q-tab-panel name="res">
 <q-list separator>
  <q-item v-for="r in res" @click="show_logs(r.no)" clickable>
   <q-item-section>
    <q-item-label>{{r.skuName}}</q-item-label>
    <q-item-label caption>{{tags.my.startUse}}:{{r.start}}</q-item-label>
   </q-item-section>
   <q-item-section side>
    <q-item-label>{{r.no}}</q-item-label>
    <q-item-label caption>{{r.inDate}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
 <div class="q-pa-sm flex flex-center" v-show="resCtrl.max>1">
  <q-pagination v-model="resCtrl.cur" color="primary" :max="resCtrl.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_res"></q-pagination>
 </div>
</q-tab-panel>

<q-tab-panel name="event">
 <q-list separator dense>
  <q-item v-for="e in events">
   <q-item-section>{{e.at}}</q-item-section>
   <q-item-section>{{e.type}}</q-item-section>
   <q-item-section>
    <q-item-label v-if="e.val!=0">{{e.val}}</q-item-label>
    <q-item-label>{{e.cmt}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
 <div class="q-pa-sm flex flex-center" v-show="evtPg.max>1">
  <q-pagination v-model="evtPg.cur" color="primary" :max="evtPg.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_event"></q-pagination>
 </div>
</q-tab-panel>

</q-tab-panels>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="resCtrl.dlg" seamless position="bottom">
 <q-card style="min-width:70vw">
  <q-card-section class="q-pt-none">
  <q-list dense>
   <q-item v-for="l in resCtrl.logs">
    <q-item-section>{{l.start}} -> {{l.end}}</q-item-section>
    <q-item-section side>{{l.account}}</q-item-section>
   </q-item>
  </q-list>
  <div v-if="resCtrl.move" class="row items-center">
   <div class="col-3">{{tags.my.moveFrom}}:{{resCtrl.move}}</div>
   <div class="col-2">
    <q-btn :label="tags.accept" @click="accept_move" color="primary" flat dense></q-btn>
   </div>
   <div class="col-2">
    <q-btn :label="tags.reject"@click="reject_move" color="secondary" flat dense></q-btn>
   </div>
   <div class="col-2 text-right">
    <q-btn :label="tags.close" color="primary" v-close-popup flat dense></q-btn>
   </div>
  </div>
  <div v-else class="row items-center">
   <div class="col-8">
    <user-selector :accounts="resCtrl.user" :label="tags.account"
     :useid="true" :multi="false" :dense="true"></user-selector>
   </div>
   <div class="col-2">
    <q-btn :label="tags.my.moveTo" @click="move_to" color="primary" flat dense></q-btn>
   </div>
   <div class="col-2 text-right">
    <q-btn :label="tags.close" color="primary" v-close-popup flat dense></q-btn>
   </div>
  </div>
  </q-card-section>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
`
}