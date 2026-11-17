import AlertDialog from "/assets/v3/components/alert_dialog.js"
import UserInput from "/assets/v3/components/user_input.js"
const EMPTY_PLAN={pid:0,start_s:'',end_s:'',stage:'',cmt:''};
const EMPTY_MEMBER={pid:0,account:{id:-1,account:''},role:''};
const EMPTY_TARGET={pid:0,base:'',challenge:'',name:'',cmt:''};
const EMPTY_PRJ={name:'',cmt:'',scope:'',start:'',end:'',type:'',leader:[]};

export default {
inject:["ibf"],
components:{
    "alert-dialog" : AlertDialog,
    "user-input" : UserInput
},
data() {return {
    pid:this.$route.query.id,
    prj:{}, //项目详情
    editable:false, //项目是否可编辑
    showAdd:false,
    isLeader:false,
    tags:this.ibf.tags,
    tab:'plan', //plan,target,member,subs
    members:[],//计划
    mbrEvents:[], //成员事件
    plans:[],//计划
    targets:[], //目标
    subs:[], //子项目
    edt:{plan:{},target:{},member:{},prj:{}},
    ctrl:{no:-2,tag:'',memberDlg:false,targetDlg:false,planDlg:false,prjDlg:false},
    opts:{stage:[],role:[],type:[]}
}},
created(){
    for(var s in this.tags.prj.roleCfg) {
        this.opts.role.push({label:this.tags.prj.roleCfg[s],value:s})
    }
    for(var i in this.tags.prj.typeCfg) {
        this.opts.type.push({label:this.tags.prj.typeCfg[i],value:i});
    }
    request({method:'GET',url:'/project/detail?id='+this.pid}, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.prj=resp.data;
        var dt=new Date();
        dt.setTime(this.prj.start*60000);
        this.prj.start_s=date2str(dt); //用于输入计划时限制时间范围
        dt.setTime(this.prj.end*60000);
        this.prj.end_s=date2str(dt);
        this.isLeader=this.prj.role=='L';
        this.editable=this.isLeader&&this.prj.stage==this.ibf.PrjStage.init;
        this.showAdd=this.editable;
        this.query_plans(); //依赖this.editable
    })
},
methods:{
tab_changed(tab) {
    this.showAdd=this.editable;
    if(tab=='plan') {
        if(this.plans.length==0) {
            this.query_plans();
        }
    } else if(tab=='target') {
        if(this.targets.length==0) {
            this.query_targets();
        }
    } else if(tab=='member'){
        this.showAdd=this.isLeader;
        if(this.members.length==0) {
            this.query_members();
        }
    } else {
        if(this.subs.length==0) {
            this.query_subs();
        }       
    }
},
show_add() {
    if(this.tab=='plan') {
        this.show_plan(-2);
    } else if(this.tab=='target') {
        this.show_target(-2);
    } else if(this.tab=='member'){
        this.show_member(-2);
    } else {
        this.show_prj(-2); //创建子项目
    }
},
query_plans() {
    var opts={method:"GET", url:"/project/plans?pid="+this.pid}
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.plans=[];
            return;
        }
        var dt=new Date();
        var plans=[];
        var Stages=this.ibf.PrjStage;
        var States=this.ibf.PlanState;
        var stage;
        for(var p of resp.data.list) {
            dt.setTime(p.start*60000);
            p.start_s=date2str(dt);
            dt.setTime(p.end*60000);
            p.end_s=date2str(dt);
            if(p.realEnd>0) {
                dt.setTime(p.realEnd*60000);
                p.realEnd_s=date2str(dt);
            } else {
                p.realEnd_s="0000/00/00";
            }
            //INIT未完成，NORM正常完成，ADVA提前完成，DELA延迟完成，CANC取消
            p.editable=p.state==States.init;
            p.rmvable=this.editable&&p.stage!=Stages.start&&p.stage!=Stages.end;
            //阶段:内置了INIT、START,RUN(可以自定义)、END、CANC
            stage=this.tags.prj.stageCfg[p.stage];
            p.stage_s=stage?stage:p.stage;
            p.state=this.tags.prj.planSta[p.state];
            plans.push(p);
        }
        this.plans=plans;
    })
},
query_targets() {
    var opts={method:"GET", url:"/project/targets?pid="+this.pid}
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.targets=[];
            return;
        }
        //type,base,challenge,real,name,cmt,state
        this.targets=resp.data.list.map((t)=>{
            t.state_s=this.tags.prj.targetSta[t.state];
            t.editable=t.state=='INIT'&&this.editable;
            return t;
        });
    })
},
query_members() {
    var opts={method:"GET", url:"/member/list?pid="+this.pid}
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.members=[];
            return;
        }
        var mbrs=[];
        var r;
        for(var m of resp.data.list) {
            r=this.tags.prj.roleCfg[m.role];
            m.role_s=r?r:m.role;
            mbrs.push(m);
        }
        this.members=mbrs;
    })
},
query_subs() {
    var opts={method:"GET", url:"/project/subs?id="+this.pid}
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.subs=[];
            return;
        }
        var stage;
        var dt=new Date();
        var prjs=[];
        var Stages=this.ibf.PrjStage;
        for(var l of resp.data.list) {
            dt.setTime(l.start*60000);
            l.start_s=date2str(dt);
            dt.setTime(l.end*60000);
            l.end_s=date2str(dt);
            stage=this.tags.prj.stageCfg[l.stage];
            l.stage_s=stage?stage:l.stage;
            l.type_s=this.tags.prj.typeCfg[l.type];
            l.editable=l.stage!=Stages.end&&l.stage!=Stages.cancel;
            l.rmvable=l.stage==Stages.init;
            prjs.push(l);
        }
        this.subs=prjs;
    })
},
query_mbrEvents(acc) {
    var opts={method:"GET", url:"/member/getPrjEvent?pid="+this.pid+"&account="+acc}
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.mbrEvents=[];
            return;
        }
        var dt=new Date();
        this.mbrEvents=resp.data.list.map(e=>{
            dt.setTime(e.at*60000);
            return {cmt:e.cmt,at:date2str(dt)};
        });
    })
},
show_plan(i) {
    if(i>-1) {
        this.ctrl.tag=this.tags.modify;
        copyObjTo(this.plans[i], this.edt.plan);
    } else {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_PLAN, this.edt.plan);
    }
    this.ctrl.tag+=this.tags.prj.plan;
    this.ctrl.no=i;
    this.ctrl.planDlg=true;
},
plan_do(act) {
    var opts;
    this.edt.plan.pid=this.pid;
    this.edt.plan.start=new Date(this.edt.plan.start_s).getTime()/60000;
    this.edt.plan.end=new Date(this.edt.plan.end_s).getTime()/60000;
    if(this.ctrl.no>-1) {
        if(act=='update') {
            var dta=copyObj(this.edt.plan,['pid','stage','start','end','cmt']);
            opts={method:"PUT",url:"/project/updatePlan",data:dta};
        } else if(act=='cancel') {
            var dta=copyObj(this.edt.plan,['pid','stage','cmt']);
            opts={method:"PUT",url:"/project/cancelPlan",data:dta};
        } else if(act=='finish') {
            var dta=copyObj(this.edt.plan,['pid','stage','cmt']);
            opts={method:"PUT",url:"/project/finishPlan",data:dta};
        } else if(act=='remove') {
            opts={method:"DELETE",url:"/project/removePlan?pid="+this.pid+"&stage="+this.edt.plan.stage};
        } else {
            return;
        }
    } else {
        opts={method:"POST",url:"/project/addPlan",data:this.edt.plan};
    }
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_plans();
        this.ctrl.no=-2;
        this.ctrl.planDlg=false;
    });
},
show_member(i) {
    if(i>-1) {
        this.ctrl.tag=this.tags.modify;
        copyObjTo(this.members[i], this.edt.member);
        this.query_mbrEvents(this.edt.member.account);
    } else {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_MEMBER, this.edt.member);
    }
    this.ctrl.tag+=this.tags.prj.member;
    this.ctrl.no=i;
    this.ctrl.memberDlg=true;
},
member_do(act) {
    this.edt.member.pid=this.pid;
    var opts;
    if(act=='remove') {
        opts={method:"DELETE",url:"/api/member/remove?pid="+this.pid+"&account="+this.etd.member.account};
    } else if(act=='appraise') {
        var dta=copyObj(this.edt.member,["pid","account","cmt"]);
        opts={method:"POST",url:"/api/member/addPrjEvent",data:dta};
    } else {
        var dta=copyObj(this.edt.member,["pid","role"]);
        dta.account=this.edt.member.account.account;
        opts={method:"POST",url:"/member/add", data:dta};
    }
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_members();
        this.ctrl.no=-2;
        this.ctrl.memberDlg=false;
    });
},
show_target(i) {
    if(i>-1) {
        this.ctrl.tag=this.tags.modify;
        copyObjTo(this.targets[i], this.edt.target);
    } else {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_TARGET, this.edt.target);
    }
    this.ctrl.tag+=this.tags.prj.target;
    this.ctrl.no=i;
    this.ctrl.targetDlg=true;
},
target_do(act) {
    var opts;
    this.edt.target.pid=this.pid;
    if(this.ctrl.no>-1) {
        if(act=='update') {
            var dta=copyObj(this.edt.target,['pid','base','challenge','cmt']);
            dta.newName=this.edt.target.name;
            dta.name=this.targets[this.ctrl.no].name;
            opts={method:"PUT",url:"/project/updateTarget",data:dta};
        } else if(act=='finish') {
            var dta=copyObj(this.edt.target,['pid','name','real','cmt']);
            opts={method:"PUT",url:"/project/finishTarget",data:dta};
        } else if(act=='remove') {
            opts={method:"DELETE",url:"/project/removeTarget?pid="+this.pid+"&name="+this.edt.target.name};
        } else {
            return;
        }
    } else {
        opts={method:"POST",url:"/project/addTarget",data:this.edt.target};
    }
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_targets();
        this.ctrl.no=-2;
        this.ctrl.targetDlg=false;
    });
},
show_prj(i) {
    if(i>-1) {
        this.ctrl.tag=this.tags.modify;
        copyObjTo(this.subs[i], this.edt.prj);
    } else {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_PRJ, this.edt.prj);
    }
    this.ctrl.tag+=this.tags.prj.subPrj;
    this.ctrl.no=i;
    this.ctrl.prjDlg=true;
},
prj_do(act) {
    var opts;
    if(act=='remove') {
        opts={method:"DELETE",url:"/project/remove?id="+this.edt.prj.id};
    } else if(act=='finish') {
        opts={method:"PUT",url:"/project/cancel",data:{id:this.edt.prj.id}}
    } else if(act=='cancel') {
        opts={method:"PUT",url:"/project/cancel",data:{id:this.edt.prj.id}};
    } else if(act=='update') {
        var dta=copyObjExc(this.edt.prj, ["start_s", "end_s"]);
        dta.start=parseInt(new Date(this.edt.prj.start_s).getTime()/60000);
        dta.end=parseInt(new Date(this.edt.prj.end_s).getTime()/60000);
        opts={method:"PUT",url:"/project/update",data:dta};
    } else {
        var dta=copyObjExc(this.edt.prj, ["start_s", "end_s"]);
        dta.start=parseInt(new Date(this.edt.prj.start_s).getTime()/60000);
        dta.end=parseInt(new Date(this.edt.prj.end_s).getTime()/60000);
        dta.leader=this.edt.prj.leader[0];
        dta.fid=this.pid;
        opts={method:"POST",url:"/project/createSub",data:dta};
    }
    request(opts, this.ibf.SERVICE_PRJ).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_subs();
        this.ctrl.no=-2;
        this.ctrl.prjDlg=false;
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.prj.title}}-{{prj.name}}</q-toolbar-title>
     <q-btn flat round icon="add_circle" dense @click="show_add()" v-show="showAdd"></q-btn>
   </q-toolbar>
  </q-header>
  <q-footer>
   <q-tabs v-model="tab" @update:model-value="tab_changed"
    dense align="justify" switch-indicator inline-label
    class="text-grey bg-grey-3" active-color="primary" indicator-color="primary">
    <q-tab name="plan" icon="assignment" :label="tags.prj.plan"></q-tab>
    <q-tab name="target" icon="flag" :label="tags.prj.target"></q-tab>
    <q-tab name="member" icon="group" :label="tags.prj.member"></q-tab>
    <q-tab name="subs" icon="account_tree" :label="tags.prj.subPrj" v-if="isLeader"></q-tab>
   </q-tabs>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-none">
<q-tab-panels v-model="tab">

<q-tab-panel name="plan">
<q-list dense separator>
  <q-item v-for="(p,i) in plans" @click="show_plan(i)" :clickable="p.editable">
    <q-item-section>
     <q-item-label>{{p.stage_s}}</q-item-label>
     <q-item-label>{{p.state}}({{p.realEnd_s}})</q-item-label>
    </q-item-section>
    <q-item-section>
     <q-item-label>{{p.start_s}}--{{p.end_s}}</q-item-label>
     <q-item-label caption>{{p.cmt}}</q-item-label>
    </q-item-section>
  </q-item>
</q-list>
</q-tab-panel>

<q-tab-panel name="target">
<q-list dense separator>
 <q-item v-for="(t,i) in targets" @click="show_target(i)" :clickable="t.editable">
  <q-item-section>
   <q-item-label>{{t.name}}</q-item-label>
   <q-item-label caption>{{t.base}}--{{t.challenge}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{t.real}}</q-item-label>
   <q-item-label caption>{{t.cmt}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
</q-tab-panel>

<q-tab-panel name="member">
 <q-list dense separator>
  <q-item v-for="(m,i) in members" @click="show_member(i)" clickable>
   <q-item-section>{{m.account}}</q-item-section>
   <q-item-section>{{m.role_s}}</q-item-section>
  </q-item>
 </q-list>
</q-tab-panel>

<q-tab-panel name="subs">
 <q-list dense separator>
  <q-item v-for="(p,i) in subs" @click="show_prj(i)" :clickable="p.editable">
   <q-item-section>
    <q-item-label>{{p.name}}({{p.type_s}})</q-item-label>
    <q-item-label caption>{{p.start_s}}-{{p.end_s}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{p.stage_s}}</q-item-label>
    <q-item-label caption>{{p.scope}}</q-item-label>
    <q-item-label caption>{{p.cmt}}</q-item-label>
   </q-item-section>
  </q-item>
 </q-list>
</q-tab-panel>

</q-tab-panels>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.planDlg" no-focus>
 <q-card style="min-width:70vw">
  <q-card-section><div class="text-h6">{{ctrl.tag}}</div></q-card-section>
  <q-card-section class="q-pt-none">
   <q-input v-model="edt.plan.stage" :label="tags.prj.stage" :disable="ctrl.no>-1" dense></q-input>
   <date-input :close="tags.ok" :label="tags.prj.start"
    v-model="edt.plan.start_s" :min="prj.start_s" :max="prj.end_s" :disable="!editable"></date-input>
   <date-input :close="tags.ok" :label="tags.prj.end"
    v-model="edt.plan.end_s" :min="prj.start_s" :max="prj.end_s" :disable="!editable"></date-input>
   <q-input :label="tags.cmt" v-model="edt.plan.cmt" type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn v-if="ctrl.no<0" :label="tags.ok" color="primary" @click="plan_do"></q-btn>
    <q-btn-dropdown v-else :label="tags.opr" color="primary" split disable-main-btn dense>
     <q-list dense>
      <q-item clickable v-close-popup @click="plan_do('update')" v-if="editable">
       <q-item-section avatar>
         <q-icon name="edit" color="primary"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.modify}}</q-item-section>
      </q-item>
      <q-item clickable v-close-popup @click="plan_do('finish')">
       <q-item-section avatar>
         <q-icon name="done" color="green"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.prj.finish}}</q-item-section>
      </q-item>
      <q-item clickable v-close-popup @click="plan_do('cancel')" v-if="edt.plan.rmvable">
       <q-item-section avatar>
         <q-icon name="remove_road" color="teal"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.cancel}}</q-item-section>
      </q-item>
      <q-item clickable v-close-popup @click="plan_do('remove')" v-if="edt.plan.rmvable">
       <q-item-section avatar>
         <q-icon name="delete" color="red"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.remove}}</q-item-section>
      </q-item>
     </q-list>
   </q-btn-dropdown>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="ctrl.targetDlg" no-focus>
 <q-card style="min-width:70vw">
  <q-card-section><div class="text-h6">{{ctrl.tag}}</div></q-card-section>
  <q-card-section class="q-pt-none">
    <q-input :label="tags.name" v-model="edt.target.name" :disable="!editable"></q-input>
    <q-input :label="tags.prj.base" v-model.number="edt.target.base" :disable="!editable"></q-input>
    <q-input :label="tags.prj.challenge" v-model.number="edt.target.challenge" :disable="!editable"></q-input>
    <q-input v-if="!editable" :label="tags.prj.real" v-model.number="edt.target.real"></q-input>
    <q-input :label="tags.cmt" v-model="edt.target.cmt" type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
     <q-btn v-if="ctrl.no<0" :label="tags.ok" color="primary" @click="target_do"></q-btn>
     <q-btn-dropdown v-else :label="tags.opr" color="primary" split disable-main-btn dense>
       <q-list dense>
        <q-item clickable v-close-popup @click="target_do('update')" v-if="editable">
         <q-item-section avatar>
           <q-icon name="edit" color="primary"></q-icon>
         </q-item-section>
         <q-item-section>{{tags.modify}}</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click="target_do('finish')" v-if="!editable">
         <q-item-section avatar>
           <q-icon name="flag" color="deep-orange"></q-icon>
         </q-item-section>
         <q-item-section>{{tags.prj.finish}}</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click="target_do('remove')" v-if="edt.target.editable">
         <q-item-section avatar>
           <q-icon name="delete" color="red"></q-icon>
         </q-item-section>
         <q-item-section>{{tags.remove}}</q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="ctrl.memberDlg">
 <q-card style="min-width:70vw">
  <q-card-section><div class="text-h6">{{ctrl.tag}}</div></q-card-section>
  <q-card-section class="q-pt-none">
   <div v-if="ctrl.no>-1">
    <q-list dense>
     <q-item>
      <q-item-section side>{{tags.prj.account}}</q-item-section>
      <q-item-section>{{edt.member.account}}</q-item-section>
     </q-item>
     <q-item>
      <q-item-section side>{{tags.prj.mbrRole}}</q-item-section>
      <q-item-section>{{edt.member.role_s}}</q-item-section>
     </q-item>
     <q-item>
      <q-item-section side>{{tags.cmt}}</q-item-section>
      <q-item-section>
       <q-input v-model="edt.member.cmt" type="textarea" rows="2"></q-input>
      </q-item-section>
     </q-item>
    </q-list>

    <q-list dense>
     <q-item v-for="e in mbrEvents">
      <q-item-section>{{e.cmt}}</q-item-section>
      <q-item-section>{{e.at}}</q-item-section>
     </q-item>
    </q-list>
   </div>
   <div v-else>
    <user-input :label="tags.prj.account" v-model="edt.member.account" ></user-input>
    <q-select v-model="edt.member.role" :options="opts.role"
    :label="tags.prj.mbrRole" dense map-options emit-value></q-select>
   </div>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   <q-btn v-if="ctrl.no<0" :label="tags.ok" color="primary" @click="member_do"></q-btn>
   <q-btn-dropdown v-else :label="tags.opr" color="primary" split disable-main-btn dense>
    <q-list dense>
     <q-item clickable v-close-popup @click="member_do('appraise')">
      <q-item-section avatar>
       <q-icon name="add_comment" color="primary"></q-icon>
      </q-item-section>
      <q-item-section>{{tags.prj.appraise}}</q-item-section>
     </q-item>
     <q-item clickable v-close-popup @click="member_do('remove')">
      <q-item-section avatar>
       <q-icon name="delete" color="red"></q-icon>
      </q-item-section>
      <q-item-section>{{tags.remove}}</q-item-section>
     </q-item>
    </q-list>
   </q-btn-dropdown>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="ctrl.prjDlg" no-focus>
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{ctrl.tag}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input :label="tags.name" v-model="edt.prj.name" dense></q-input>
   <q-select :label="tags.prj.type" v-model="edt.prj.type" :options="opts.type"
    dense map-options emit-value></q-select>
   <date-input :close="tags.ok" :label="tags.prj.start_s" v-model="edt.prj.start_s"></date-input>
   <date-input :close="tags.ok" :label="tags.prj.end_s" v-model="edt.prj.end_s" min="today"></date-input>
   <user-selector :label="tags.prj.leader" v-if="ctrl.no<0"
    :accounts="edt.prj.leader" :multi="false"></user-selector>
   <q-input :label="tags.cmt" v-model="edt.prj.cmt" dense></q-input>
   <q-input :label="tags.prj.scope" v-model="edt.prj.scope" dense type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   <q-btn v-if="ctrl.no<0" :label="tags.ok" color="primary" @click="prj_do"></q-btn>
   <q-btn-dropdown v-if="ctrl.no>-1&&edt.prj.editable" :label="tags.opr"
    color="primary" split disable-main-btn dense>
     <q-list dense>
      <q-item clickable v-close-popup @click="prj_do('update')">
       <q-item-section avatar>
         <q-icon name="edit" color="primary"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.modify}}</q-item-section>
      </q-item>
      <q-item clickable v-close-popup @click="prj_do('cancel')">
       <q-item-section avatar>
         <q-icon name="remove_road" color="teal"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.cancel}}</q-item-section>
      </q-item>
      <q-item clickable v-close-popup @click="prj_do('remove')" v-if="edt.prj.rmvable">
       <q-item-section avatar>
         <q-icon name="delete" color="red"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.remove}}</q-item-section>
      </q-item>
     </q-list>
   </q-btn-dropdown>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
`
}