const EMPTY_PLAN={pid:0,start_s:'',end_s:'',stage:'',cmt:''};
const EMPTY_TARGET={pid:0,base:'',challenge:'',name:'',cmt:''};

export default {
inject:["ibf", "service"],
data() {return {
    pid:this.$route.query.id,
    prj:{}, //项目详情
    editable:false, //项目是否可编辑
    tags:this.ibf.tags,
    tab:'plan', //plan,target
    plans:[],//计划
    targets:[], //目标
    edt:{plan:{},target:{}},
    ctrl:{no:-2,tag:'',targetDlg:false,planDlg:false}
}},
created(){
    this.get_detail();
},
methods:{
get_detail() {
    request({method:'GET',url:'/project/detail?id='+this.pid}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.prj=resp.data;
        var dt=new Date();
        dt.setTime(this.prj.start*60000);
        this.prj.start_s=date2str(dt); //用于限制项目计划的时间范围
        dt.setTime(this.prj.end*60000);
        this.prj.end_s=date2str(dt);
        this.prj.type=this.tags.prj.typeCfg[this.prj.type];
        var stage=this.tags.prj.stageCfg[this.prj.stage];
        this.prj.stage_s=stage?stage:this.prj.stage;
        this.editable=this.prj.stage!=this.ibf.PrjStage.cancel
            &&this.prj.stage!=this.ibf.PrjStage.end;
        if(resp.data.main) {
            this.prj.owner=resp.data.main.O;
            this.prj.leader=resp.data.main.L;
        }
        this.query_plans();//依赖editable
    });
},
tab_changed(tab) {
    if(tab=='plan') {
        if(this.plans.length==0) {
            this.query_plans();
        }
    } else {
        if(this.targets.length==0) {
            this.query_targets();
        }
    }
},
show_add() {
    if(this.tab=='plan') {
        this.show_plan(-2);
    } else {
        this.show_target(-2);
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
            p.stage=stage?stage:p.stage;
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
prj_do(act) {
    var opts;
    var dta={};
    this.prj.start=parseInt(new Date(this.prj.start_s).getTime()/60000);
    this.prj.end=parseInt(new Date(this.prj.end_s).getTime()/60000);
    copyObjTo(this.prj, dta, ['id','name','cmt','scope','type','start','end']);
    if(act=='update') {
        dta.id=this.pid;
        opts={method:"PUT",url:"/project/update",data:dta};
    } else if(act=='cancel'){
        opts={method:"DELETE",url:"/project/cancel?id="+this.pid}
    } else if(act=='remove'){
        opts={method:"DELETE",url:"/project/remove?id="+this.pid};
    } else {
        return;
    }
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        if(act=='remove') {
            this.ibf.back();
            return;
        }
        this.$refs.prjDlg.hide();
        this.get_detail();
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.prj.title}}-{{prj.name}}({{prj.stage_s}})</q-toolbar-title>
     <q-btn flat icon="add_circle" dense @click="show_add()" v-if="editable"></q-btn>
     <q-btn flat icon="edit_note" dense v-if="editable">
     <q-popup-proxy ref="prjDlg">
      <q-card style="min-width:70vw">
       <q-card-section class="q-pt-none"><q-list dense>
        <q-item><q-item-section side>{{tags.name}}</q-item-section>
         <q-item-section>
          <q-input v-model="prj.name" dense></q-input>
         </q-item-section>
        </q-item>
        <q-item><q-item-section side>{{tags.prj.type}}</q-item-section>
         <q-item-section>{{prj.type}}</q-item-section>
        </q-item>
        <q-item><q-item-section side>{{tags.prj.owner}}</q-item-section>
         <q-item-section>{{prj.owner}}</q-item-section>
        </q-item>
        <q-item><q-item-section side>{{tags.prj.leader}}</q-item-section>
         <q-item-section>{{prj.leader}}</q-item-section>
        </q-item>
        <q-item><q-item-section side>{{tags.prj.start}}</q-item-section>
         <q-item-section>
          <date-input :close="tags.ok" v-model="prj.start_s"></date-input>
         </q-item-section>
        </q-item>
        <q-item><q-item-section side>{{tags.prj.end}}</q-item-section>
         <q-item-section>
          <date-input :close="tags.ok" v-model="prj.end_s"></date-input>
         </q-item-section>
        </q-item>
        <q-item><q-item-section side>{{tags.cmt}}</q-item-section>
         <q-item-section><q-input v-model="prj.cmt"></q-input></q-item-section>
        </q-item>
        <q-item><q-item-section side>{{tags.prj.scope}}</q-item-section>
         <q-item-section><q-input v-model="prj.scope"></q-input></q-item-section>
        </q-item>
       </q-list></q-card-section>
       <q-card-actions align="right">
        <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
        <q-btn-dropdown :label="tags.opr" color="primary" split disable-main-btn dense>
         <q-list dense style="min-width:100px">
          <q-item clickable v-close-popup @click="prj_do('update')">
            <q-item-section avatar><q-icon name="edit" color="primary"></q-icon></q-item-section>
            <q-item-section>{{tags.modify}}</q-item-section>
          </q-item>
          <q-item clickable v-close-popup @click="prj_do('cancel')">
            <q-item-section avatar><q-icon name="cancel" color="purple"></q-icon></q-item-section>
            <q-item-section>{{tags.prj.cancel}}</q-item-section>
          </q-item>
          <q-item clickable v-close-popup @click="prj_do('remove')" v-if="prj.stage=='INIT'">
            <q-item-section avatar><q-icon name="delete_forever" color="red"></q-icon></q-item-section>
            <q-item-section>{{tags.remove}}</q-item-section>
          </q-item>
         </q-list>
        </q-btn-dropdown>
        </q-card-actions>
      </q-card>
     <q-popup-proxy>
    </q-btn>
   </q-toolbar>
  </q-header>
  <q-footer>
   <q-tabs v-model="tab" @update:model-value="tab_changed"
    dense align="justify" switch-indicator inline-label
    class="text-grey bg-grey-3" active-color="primary" indicator-color="primary">
    <q-tab name="plan" icon="assignment" :label="tags.prj.plan"></q-tab>
    <q-tab name="target" icon="flag" :label="tags.prj.target"></q-tab>
   </q-tabs>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-sm">
<q-tab-panels v-model="tab">

<q-tab-panel name="plan">
<q-list dense separator>
  <q-item v-for="(p,i) in plans" @click="show_plan(i)" :clickable="p.editable">
    <q-item-section>
     <q-item-label>{{p.stage}}</q-item-label>
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

</q-tab-panels>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.planDlg">
 <q-card style="min-width:70vw">
  <q-card-section><div class="text-h6">{{ctrl.tag}}</div></q-card-section>
  <q-card-section class="q-pt-none">
   <q-input v-model="edt.plan.stage" :label="tags.prj.stage" :disable="ctrl.no>-1" dense></q-input>
   <date-input :close="tags.ok" :label="tags.prj.start"
    v-model="edt.plan.start_s" :min="prj.start_s" :max="prj.end_s"></date-input>
   <date-input :close="tags.ok" :label="tags.prj.end"
    v-model="edt.plan.end_s" :min="prj.start_s" :max="prj.end_s"></date-input>
   <q-input :label="tags.cmt" v-model="edt.plan.cmt" type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn v-if="ctrl.no<0" :label="tags.ok" color="primary" @click="plan_do"></q-btn>
    <q-btn-dropdown v-else :label="tags.opr" color="primary" split disable-main-btn dense>
     <q-list dense>
      <q-item clickable v-close-popup @click="plan_do('update')">
       <q-item-section avatar>
         <q-icon name="edit" color="primary"></q-icon>
       </q-item-section>
       <q-item-section>{{tags.modify}}</q-item-section>
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

<q-dialog v-model="ctrl.targetDlg">
 <q-card style="min-width:70vw">
  <q-card-section><div class="text-h6">{{ctrl.tag}}</div></q-card-section>
  <q-card-section class="q-pt-none">
    <q-input :label="tags.name" v-model="edt.target.name"></q-input>
    <q-input :label="tags.prj.base" v-model.number="edt.target.base" type="number"></q-input>
    <q-input :label="tags.prj.challenge" v-model.number="edt.target.challenge" type="number"></q-input>
    <q-input :label="tags.cmt" v-model="edt.target.cmt" type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
     <q-btn v-if="ctrl.no<0" :label="tags.ok" color="primary" @click="target_do"></q-btn>
     <q-btn-dropdown v-else :label="tags.opr" color="primary" split disable-main-btn dense>
       <q-list dense>
        <q-item clickable v-close-popup @click="target_do('update')">
         <q-item-section avatar>
           <q-icon name="edit" color="primary"></q-icon>
         </q-item-section>
         <q-item-section>{{tags.modify}}</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click="target_do('remove')" >
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